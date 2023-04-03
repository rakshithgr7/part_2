import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cdk from 'aws-cdk-lib';
import {readFileSync} from 'fs';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class Part2CdkStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //  s3 bucket with lifecycle transitions and KMS encryption enabled
    const bucket = new s3.Bucket(this, 'MyEncryptedBucket', {
      encryption: s3.BucketEncryption.KMS,
      versioned:true,
      bucketName:"part2asigncdklbhhgbgboo007",
      lifecycleRules: [
      {
      transitions: [
      {
      storageClass: s3.StorageClass.INFREQUENT_ACCESS,
      transitionAfter: cdk.Duration.days(30),
      },
      {
      storageClass: s3.StorageClass.GLACIER,
      transitionAfter: cdk.Duration.days(90),
      },
      ],
      },
      ],
      });
      


    //created VPC in which we'll launch the Instance
    const vpc = new ec2.Vpc(this, 'my-cdk-vpc', {
      cidr: '10.0.0.0/16',
      natGateways: 0,
      subnetConfiguration: [
        {name: 'public', cidrMask: 24, subnetType: ec2.SubnetType.PUBLIC},
      ],
    });

    // created Security Group for the Instance
    const webserverSG = new ec2.SecurityGroup(this, 'webserver-sg', {
      vpc,
      allowAllOutbound: true,
    });

    webserverSG.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(22),
      'allow SSH access from anywhere',
    );

    webserverSG.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(80),
      'allow HTTP traffic from anywhere',
    );

    webserverSG.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      'allow HTTPS traffic from anywhere',
    );

    // created a Role for the EC2 Instance
    const webserverRole = new iam.Role(this, 'webserver-role', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
      ],
    });

    //created the EC2 Instance 
    const ec2Instance = new ec2.Instance(this, 'ec2-instance', {
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC,
      },
      role: webserverRole,
      securityGroup: webserverSG,
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE2,
        ec2.InstanceSize.MICRO,
      ),
      machineImage: new ec2.AmazonLinuxImage({
        generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
      }),
      keyName: 'assignment',
    });
    bucket.grantReadWrite(ec2Instance);
    // load contents of script
    const userDataScript = readFileSync('./lib/user-data.sh', 'utf8');
    // add the User Data script to the Instance, user script as ngnix server and also changed the hostname 
    ec2Instance.addUserData(userDataScript);
  }
}